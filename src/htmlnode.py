class HTMLNode():

    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props


    def to_html(self):
        raise NotImplementedError("Subclasses should implement this method.")
    
    def props_to_html(self):
        if self.props is None:
            return ""
        result = ""
        for key, value in self.props.items():
            result += f' {key}="{value}"'
        return result
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
    def __eq__(self, other):
        if (not isinstance(other, HTMLNode)):
            return False
        if self.tag != other.tag or self.value != other.value:
            return False
        if self.children is None:
            if other.children is not None:
                return False
        else:
            for child in self.children:
                other_has_match = False
                for other_child in other.children:
                    if child == other_child:
                        other_has_match = True
                        break
                if not other_has_match: 
                    return False
        if self.props is None:
            if other.props is not None:
                return False
        return self.children == other.children
            

        
    
class LeafNode(HTMLNode):

    def __init__(self, tag, value, props=None):
        if value is None:
            raise ValueError("Leaf nodes must have a value")
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):

    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")
        elif self.children is None:
            raise ValueError("ParentNode must have a 'children' dictionary")
        result = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            result += child.to_html()
        return result + f"</{self.tag}>"