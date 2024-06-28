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
        jd = JobDescription(**validated_data)
        _output_response = send_job_description_to_api(validated_data["_input_job_description"], 'keyQuestions')
        jd._output_response = _output_response
        jd.save()
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
        formatted_qa = []
        for idx, item in enumerate(jd._output_response["questions_and_answers"], start=1):
            formatted_qa.append({
                f"Question {idx}": item["Question"].strip(),
                "Answer": item["Answer"].strip()
            })
        jd._output_response = {"questions_and_answers": formatted_qa}
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
        password = validated_data.pop("password")
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        Token.objects.create(user=user)
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
