from rest_framework import serializers, fields
from rest_framework.exceptions import ValidationError


class GitHubListSerializer(serializers.ListSerializer):
    def __init__(self, *args, **kwargs):
        self.queryset = kwargs.pop('queryset')
        super().__init__(*args, **kwargs)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def save(self, **kwargs):
        validated_data = {
            attrs['id']: {**attrs, **kwargs} for attrs in self.validated_data
        }

        updated = list()
        for instance in self.queryset:
            instance = self.update(instance, validated_data[instance.id])
            assert instance is not None, (
                '`update()` did not return an object instance.'
            )
            updated.append(instance)
            validated_data.pop(instance.id)
        created = self.create(validated_data.values())
        assert created is not None, (
            '`create()` did not return an object instance.'
        )

        return updated + created


class GitHubSerializerMixin:
    def __init__(self, instance=None, data=fields.empty, **kwargs):
        self.auto_instance = kwargs.pop('auto_instance', False)
        self.queryset = kwargs.pop('queryset', None)
        if self.auto_instance:
            assert self.queryset is not None, 'Auto instance needs a queryset'
        super().__init__(instance=instance, data=data, **kwargs)

    @classmethod
    def many_init(cls, *args, **kwargs):
        model = getattr(getattr(cls, 'Meta', None), 'model', None)
        if not all({'id' in u.keys() for u in kwargs.get('data', list())}):
            raise ValidationError({
                'id': 'id field is required for entire dataset'
            })
        queryset = model.objects.filter(
            id__in=[u['id'] for u in kwargs.get('data', list())]
        )
        kwargs['queryset'] = queryset
        kwargs['child'] = cls(
            auto_instance=kwargs.pop('auto_instance', False),
            queryset=queryset,
        )
        return GitHubListSerializer(*args, **kwargs)

    def run_validation(self, data=fields.empty):
        if self.auto_instance:
            self.instance = self.queryset.filter(id=data['id']).first()
        return super().run_validation(data=data)
