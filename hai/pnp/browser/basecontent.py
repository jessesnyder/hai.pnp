from Products.Five.browser import BrowserView

class BasePnPView(BrowserView):
    """ A basic view of HAI Policy and Procedure Content """
    
    def __call__(self):
        pass
    
    def test(self):
        return "working"

    def getLastVisited(self,formattedString=None):
        if formattedString is None:
            return []
        tokens = formattedString.split('||')
        if len(tokens) < 2:
            return []
        return tokens
    
    def getLinkFromToken(self, token='blank!blank'):
        bits = token.split('!')
        if len(bits) > 1:
            return bits[1]

    def getIdFromToken(self, token='blank!blank'):
        bits = token.split('!')
        if len(bits) > 1:
            return bits[0]

    def createLastVisited(self,formattedString=None):
        if formattedString is None:
            return self.context.absolute_url()
        else:
            tokens = formattedString.split('||')
            newest = self.context.Title() + '!' + self.context.absolute_url()
            # if this item is already in our history, truncate the history list back at that point instead of dup'ing
            if newest in tokens:
                tokens = tokens[:(tokens.index(newest))]
            tokens.append(newest)
            excess = len(tokens) - 5
            if(excess > 0):
                tokens = tokens[excess:]
            return '||'.join(tokens)
