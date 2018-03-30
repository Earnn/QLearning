# in project/app/context_processors.py
from mainapp.models import Profile

def profile(request):
	profile_picture=""
	try :
		profile_picture = Profile.objects.get(user=request.user).picture.url

	except:
		pass
	return {'profile': profile_picture} # of course some filter here


def profile_name(request):
	profile_name=""
	try :
	
		profile_name =  Profile.objects.get(user=request.user).name
		print("profile_name",profile_name)
	except:
		pass
	return {'profile_name':profile_name} # of course some filter here	



def isOwnerShop(request):
	profile_name=""
	try :
	
		store =  StoreByUser.objects.get(user=request.user)
		print("profile_name",profile_name)
	except StoreByUser.DoesNotExist:
		store = None
	return {'userstore':store} # of course some filter here		