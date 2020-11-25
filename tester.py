import os

def initializeFS():
        """initialize filesystem for storing stuff                                                                                                                                                                                                                                                                                                                                            
        :returns: success bool"""
        print(os.name)
        if (os.name == "posix"):
                home = os.path.expanduser("~")
                if (not (os.path.exists(home+"/.cmpt370checkerschess"))):
                        os.mkdir(home+"/.cmpt370checkerschess")
                return 1
        elif (os.name == "nt"):
                app_data = os.getenv("LOCALAPPDATA")
                if (not (os.path.exists(app_data+"/.cmpt370checkerschess"))):
                        os.mkdir(app_data+"/.cmpt370checkerschess")
                return 1
        else:
                print("uknown os")
        
if __name__=="__main__":
        initializeFS();
        
