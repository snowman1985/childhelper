'''
Created on 2014年1月12日

@author: shengeng
'''

def auth_user(request):
    try:
        user = request.user
        if user.is_authenticated:
            return(True, user.username, user.password, user)
        else:
            return(False, None, None, None)
    except Exception as e:
        return(False, None, None, None)
        
