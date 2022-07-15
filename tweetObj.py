class TwitterObj ():
    id = 0
    text = ""
    posi = 0
    nega = 0
    neutral = 0
    
    def __init__ (self, id, text):
        self.id = id
        self.text = text
        
    def setPosi(self , posi):
        self.posi = posi
    
    def getPosi(self):
        return self.posi
    
    def setNeutral(self , neutral):
        self.neutral = neutral
    
    def getNeutral(self):
        return self.neutral
    
    def setNega(self , nega):
        self.nega = nega
    
    def getNega(self):
        return self.nega
    
    def getId(self):
        return self.id
    
    def getText(self):
        return self.text
    

    
