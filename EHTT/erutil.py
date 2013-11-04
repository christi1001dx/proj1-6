
error = -1
errorbox = {-1:"no error",
             0:"Field missing",
             1:"Error101: User not found",
             2:"Username or password incorrect",
             3:"Username exists",
             4:"Error404: Post not found",
             5:"Post name already exists",
}

def errorlook():
    return errorbox[error]
def errorch(num):
    error = num
    print(error)
