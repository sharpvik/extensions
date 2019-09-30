const doc = document;
function $(q) { return doc.querySelector(q); }



window.colors = [
    '#F44336', '#D50000', '#E91E63', '#880E4F', '#9C27B0', '#4A148C', '#673AB7',
    '#311B92', '#3F51B5', '#1A237E', '#2196F3', '#0D47A1', '#03A9F4', '#01579B',
    '#00BCD4', '#006064', '#009688', '#004D40', '#4CAF50', '#1B5E20', '#8BC34A',
    '#CDDC39', '#827717', '#FFEB3B', '#F57F17', '#FFC107', '#FF6F00', '#FF9800',
    '#E65100', '#FF5722', '#BF360C', '#795548', '#3E2723', '#9E9E9E', '#607D8B',
    '#263238'
];
window.usedColors = [];



// toggle switches on and off
doc.addEventListener('click', function(e) {
    var trg;
    if ( e.target.matches('.switch') ) trg = e.target;
    else if ( e.target.matches('.toggler') ) trg = e.target.parentElement;
    else return;
    var cls = trg.classList.contains('switch-on') ? 'switch-off' : 'switch-on';

    trg.classList.remove('switch-on');
    trg.classList.remove('switch-off');
    trg.classList.add(cls);
}, false);

// analyse on submit
$('#submit').addEventListener('click', function(e) {
    e.preventDefault();

    var path = $('#path').value,
        r = $('#r').classList.contains('switch-on'),
        cwd = $('#cwd').classList.contains('switch-on');

    eel.set_recursive(r);
    if (cwd) eel.analyse()(render);
    else eel.analyse(path)(render);
});

// render results (used as callback function)
eel.expose(render);
function render(results, total) {
    // clear chart and results
    $('#colors').innerHTML = '';
    $('#results').innerHTML = '';
    window.usedColors = [];

    var dict = results[0],
        total = results[1];

    Object.keys(dict).forEach(function(key) {
        var number = dict[key],
            percent = number / total * 100;

        // select a color for this extention
        var index = randInt(window.colors.length);
        while (index in window.usedColors)
            index = randInt(window.colors.length);
        window.usedColors.push(index);
        
        // add an .extention to main#colors (do it through the slice object)
        var styles = new StylesObject();
        styles.addRule('background-color', window.colors[index]);
        styles.addRule( 'width', percent.toString() + '%' );

        var extention = new HtmlElement('div', 'extention', styles, '');
        $('#colors').innerHTML += extention.getHtmlCode();

        
        // add a .result-line to main#results
        /*
            <div class="result-line">
                    <div class="color-thumbnail"></div>
                    <span class="extention">JavaScript -- 42 file(s)</span>
                </div>
            </div>
        */
        var colorThumbnailStyles = new StylesObject();
        colorThumbnailStyles.addRule('background-color', window.colors[index]);
        var colorThumbnail = new HtmlElement(
            'div',
            'color-thumbnail',
            colorThumbnailStyles,
            ''
        );
        var extentionLine = new HtmlElement(
            'span',
            'extention',
            new StylesObject(),
            key + ' -- ' + number + ' file(s)'
        );
        var resultLine = new HtmlElement(
            'div', 
            'result-line',
            new StylesObject(),
            colorThumbnail.getHtmlCode() + extentionLine.getHtmlCode()
        );

        $('#results').innerHTML += resultLine.getHtmlCode();
    });
}
