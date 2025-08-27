from core.config import getConfig, setConfig

class SettingsManager():
    def __init__(self) -> None:
        pass

    def saveUserinfoSettings(self,username,password,profile):
        """
        保存用户信息
        """
        config = getConfig()
        if config["USER"]["USERNAME"]=="":
            return self.customerSaveUserInfo(profile)
        else:
            return self.saveUserInfo(username,password,profile)
        
    
    def saveUserInfo(self,username,password,profile):
        """
        TODO: 保存用户信息,同步云端
        """
        if username and password:
            return True
        else:
            return False

    def customerSaveUserInfo(self,profile):
        """
        游客模式保存profile
        """
        config = getConfig()
        config["USER"]["PERSONALPROFILE"] = profile
        setConfig(config)
        return True

    def saveRemoteSettings(self,remoteUrl):
        """
        保存服务器链接
        """
        config = getConfig()
        config["REMOTE"]["URL"] = remoteUrl
        setConfig(config)

    def saveModelSettings(self,provider,url,model,api_key,genScorePrompt):
        """
        保存模型请求信息，一般是本地化服务，分数的生成由远端进行
        """
        config = getConfig()
        config["LLM"]["PROVIDER"] = provider
        config["LLM"]["URL"] = url
        config["LLM"]["MODEL_NAME"] = model
        config["LLM"]["API_KEY"] = api_key
        config["LLM"]["genScorePrompt"] = genScorePrompt
        setConfig(config)

    def saveTheme(self,compo:str,colorName:str):
        """
        保存主题颜色，compo代表需要更改的组件，包括：
        btn,btnHover,bg,font
        """
        config = getConfig()
        if compo == "btn":
            config["THEME"]["BTNCOLOR"] = colorName
        elif compo == "btnHover":
            config["THEME"]["BTNHOVERCOLOR"] = colorName
        elif compo == "bg":
            config["THEME"]["BGCOLOR"] = colorName
        elif compo == "font":
            config["THEME"]["FONTCOLOR"] = colorName
        setConfig(config)

    def getSettings(self):
        return getConfig()