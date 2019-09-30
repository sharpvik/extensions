// constructors
function StylesObject() {
    this.registry = {};

    this.addRule = function(prop, value) {
        this.registry[prop] = value;
    };

    this.getHtmlCode = function() {
        var $this = this;
            htmlCode = 'style="';
        Object.keys(this.registry).forEach(function(key) {
            htmlCode += key + ': ' + $this.registry[key] + ';';
        });
        htmlCode += '"';
        return htmlCode;
    };
}

function HtmlElement(tag, classes, styles, contents) {
    var $this = this;

    this.tag = tag;
    this.classes = classes;
    this.styles = styles;
    this.contents = contents;

    this.getHtmlCode = function() {
        return '<' + this.tag + ' ' + 'class="' + this.classes + '"' + 
               this.styles.getHtmlCode() + '>' + this.contents + '</' + 
               this.tag + '>';
    };
}



// functions
function randInt(max) {
    return Math.floor(Math.random() * Math.floor(max));
}