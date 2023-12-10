from rest_framework import serializers
from .models import MyUser, Role, Permission

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'




class PermissionRelatedField(serializers.StringRelatedField):
    def to_representation(self, value):
        return PermissionSerializer(value).data

    def to_internal_value(self, data):
        return data



class RoleSerializer(serializers.ModelSerializer):
    permissions = PermissionRelatedField(many=True)
    class Meta:
        model = Role
        fields = '__all__'

    def create(self, validated_data):

        permissions = validated_data.pop('permissions', None)
        instance = self.Meta.model(**validated_data)

        instance.save()
        instance.permissions.add(*permissions)
        instance.save()
        return instance


class RoleRelatedField(serializers.RelatedField):
    def to_representation(self, instance):
        print('Role ', instance)
        return RoleSerializer(instance).data

    def to_internal_value(self, data):
        return self.queryset.get(pk=data)


class UserSerializer(serializers.ModelSerializer):
    role = RoleRelatedField(many=False, queryset=Role.objects.all())
    class Meta:
        model = MyUser
        fields = ['id','first_name','last_name','email','password','username', 'role','order_num']
        extra_kwargs = {
            'password': {'write_only': True }
        }

    def create(self,validated_data):
        print('validated_data: ', validated_data)
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password is not None:
            instance.set_password(password)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.role = validated_data.get('role', instance.role)
        instance.save()
        return instance



