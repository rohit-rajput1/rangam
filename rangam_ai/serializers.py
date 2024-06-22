from rest_framework import serializers
from rangam_ai.models import JobDescription, JobSkillsRequired, JobQuestionsRequired, JobKeyResponsibilitiesRequired
from django.contrib.auth.models import User
from rangam_ai.utils import send_job_description_to_api
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

class JobDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobDescription
        fields = ("id", "_input_job_description", "_output_response")
        extra_kwargs = {"_output_response": {"read_only": True}}

    def create(self, validated_data):
        # Initialize a new JobDescription object with the validated data
        jd = JobDescription(**validated_data)
        
        # Send the input job description to the external API and get the response
        _output_response = send_job_description_to_api(validated_data["_input_job_description"])
        
        # Set the output response on the JobDescription object
        jd._output_response = _output_response
        
        # Save the JobDescription object to the database
        jd.save()
        
        # Return the saved JobDescription object
        return jd

class JobSkillsRequiredSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSkillsRequired
        fields = ("id", "_input_job_description", "_output_response")
        extra_kwargs = {"_output_response": {"read_only": True}}

    def create(self, validated_data):
        jd = JobSkillsRequired(**validated_data)
        jd._output_response = send_job_description_to_api(validated_data["_input_job_description"], 'keySkills')
        jd.save()
        return jd


class JobQuestionsRequiredSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobQuestionsRequired
        fields = ("id", "_input_job_description", "_output_response")
        extra_kwargs = {"_output_response": {"read_only": True}}

    def create(self, validated_data):
        jd = JobQuestionsRequired(**validated_data)
        jd._output_response = send_job_description_to_api(validated_data["_input_job_description"], 'keyQuestions')
        jd.save()
        return jd


class JobKeyResponsibilitiesRequiredSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobKeyResponsibilitiesRequired
        fields = ("id", "_input_job_description", "_output_response")
        extra_kwargs = {"_output_response": {"read_only": True}}

    def create(self, validated_data):
        jd = JobKeyResponsibilitiesRequired(**validated_data)
        jd._output_response = send_job_description_to_api(validated_data["_input_job_description"], 'keyResponsibilities')
        jd.save()
        return jd

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}
    
    def create(self, validated_data):
        # Extract the password from validated data
        password = validated_data.pop("password")
        
        # Create a new User object with the remaining data
        user = User.objects.create(**validated_data)
        
        # Set the user's password (hashing it)
        user.set_password(password)
        
        # Save the user object to the database
        user.save()
        
        # Create an authentication token for the user
        Token.objects.create(user=user)
        
        # Return the newly created user object
        return user

class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={"input_type": "password"}, trim_whitespace=False)

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")
        user = authenticate(request=self.context.get("request"), username=username, password=password)
        if not user:
            msg = "Unable to authenticate with provided credentials"
            raise serializers.ValidationError(msg, code="authorization")
        attrs["user"] = user
        return attrs
