from rest_framework import views,status
from rest_framework.response import Response
from django.contrib.auth.models import User
from rangam_ai.serializers import JobDescriptionSerializer,UserSerializer,TokenSerializer, JobSkillsRequiredSerializer,JobQuestionsRequiredSerializer ,JobKeyResponsibilitiesRequiredSerializer
from rangam_ai.models import JobDescription,JobSkillsRequired, JobQuestionsRequired, JobKeyResponsibilitiesRequired
from rest_framework.authtoken.views  import ObtainAuthToken
from rest_framework.authentication import TokenAuthentication

class JobDescriptionView(views.APIView):
    # defining the serializer class for the view class
    serializer_class = JobDescriptionSerializer
    authentication_classes = [TokenAuthentication]

    # This API will have get and post requests
    def get(self,request,format=None):
        # here we will make a query set to get all the job descriptions ana save it in qs
        qs  = JobDescription.objects.all()
        serializer = self.serializer_class(qs,many=True)
        return Response(serializer.data)

    def post(self,request,format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class JobSkillsRequiredView(views.APIView):
    serializer_class = JobSkillsRequiredSerializer
    authentication_classes = [TokenAuthentication]

    def get(self, request, format=None):
        qs = JobSkillsRequired.objects.all()
        serializer = self.serializer_class(qs, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JobQuestionsRequiredView(views.APIView):
    serializer_class = JobQuestionsRequiredSerializer
    authentication_classes = [TokenAuthentication]

    def get(self, request, format=None):
        qs = JobQuestionsRequired.objects.all()
        serializer = self.serializer_class(qs, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JobKeyResponsibilitiesRequiredView(views.APIView):
    serializer_class = JobKeyResponsibilitiesRequiredSerializer
    authentication_classes = [TokenAuthentication]

    def get(self, request, format=None):
        qs = JobKeyResponsibilitiesRequired.objects.all()
        serializer = self.serializer_class(qs, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Now we will create the User View to handle, When the client make request to user endpoint.
class UserView(views.APIView):
    serializer_class = UserSerializer
    def get(self,request,format=None):
        qs = User.objects.all()
        serializer = self.serializer_class(qs,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self,request,format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class TokenView(ObtainAuthToken):
    serializer_class = TokenSerializer