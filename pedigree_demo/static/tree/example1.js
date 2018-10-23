var labelType, useGradients, nativeTextSupport, animate;

(function () {
    var ua = navigator.userAgent,
        iStuff = ua.match(/iPhone/i) || ua.match(/iPad/i),
        typeOfCanvas = typeof HTMLCanvasElement,
        nativeCanvasSupport = (typeOfCanvas == 'object' || typeOfCanvas == 'function'),
        textSupport = nativeCanvasSupport
            && (typeof document.createElement('canvas').getContext('2d').fillText == 'function');
    //I'm setting this based on the fact that ExCanvas provides text support for IE
    //and that as of today iPhone/iPad current text support is lame
    labelType = (!nativeCanvasSupport || (textSupport && !iStuff)) ? 'Native' : 'HTML';
    nativeTextSupport = labelType == 'Native';
    useGradients = nativeCanvasSupport;
    animate = !(iStuff || !nativeCanvasSupport);
})();

var Log = {
    elem: false,
    write: function (text) {
        if (!this.elem)
            this.elem = document.getElementById('log');
        this.elem.innerHTML = text;

    }
};


function init() {
    //init data
    var json = {
        id: "node02",
        name: "0.2",
        data: {'name': 'DOGGY'},
        children: [{
            id: "node11",
            name: "1.1",
            data: {},
            children: []
        },
        {
            id: "node12",
            name: "1.2",
            data: {},
            children: []
        }]
    };
    //end
    //init Spacetree
    //Create a new ST instance
    var st = new $jit.ST({
        //id of viz container element
        injectInto: 'infovis',
        //set duration for the animation
        duration: 300,
        //set animation transition type
        transition: $jit.Trans.Quart.easeInOut,
        //set distance between node and its children
        levelDistance: 50,
        //enable panning
        Navigation: {
            enable: true,
            panning: true
        },
        //set node and edge styles
        //set overridable=true for styling individual
        //nodes or edges
        Node: {
            height: 270,
            width: 332,
            type: 'rectangle',
            color: '#343a40',
            overridable: true
        },

        Edge: {
            type: 'bezier',
            overridable: true
        },

        onBeforeCompute: function (node) {
            Log.write("loading " + node.name);
        },

        onAfterCompute: function () {
            Log.write("done");
        },

        //This method is called on DOM label creation.
        //Use this method to add event handlers and styles to
        //your node.
        onCreateLabel: function (label, node) {
            label.id = node.id;
            label.innerHTML += '<div class="card">\n' +
                '            <div class="card-body">\n' +
                '                <!-- Nav tabs -->\n' +
                '                <ul class="nav nav-tabs" role="tablist">\n' +
                '                    <li class="nav-item"><a class="nav-link active" data-toggle="tab" href="#info' + node.id + '" role="tab"><span\n' +
                '                            class="hidden-sm-up"><i class="ti-home"></i></span> <span\n' +
                '                            class="hidden-xs-down">Info</span></a></li>\n' +
                '                    <li class="nav-item"><a class="nav-link" data-toggle="tab" href="#bio' + node.id + '" role="tab"><span\n' +
                '                            class="hidden-sm-up"><i class="ti-user"></i></span> <span\n' +
                '                            class="hidden-xs-down">Bio</span></a></li>\n' +
                '                    <li class="nav-item"><a class="nav-link" data-toggle="tab" href="#breeder' + node.id + '" role="tab"><span\n' +
                '                            class="hidden-sm-up"><i class="ti-email"></i></span> <span\n' +
                '                            class="hidden-xs-down">Breeder</span></a>\n' +
                '                    </li>\n' +
                '                    <li class="nav-item"><a class="nav-link" data-toggle="tab" href="#owner' + node.id + '" role="tab"><span\n' +
                '                            class="hidden-sm-up"><i class="ti-email"></i></span> <span\n' +
                '                            class="hidden-xs-down">Owner</span></a></li>\n' +
                '                </ul>\n' +
                '                <!-- Tab panes -->\n' +
                '                <div class="tab-content tabcontent-border">\n' +
                '                    <div class="tab-pane active" id="info' + node.id + '" role="tabpanel">\n' +
                '                        <div class="p-20">\n' +
                '                                <div class="el-card-avatar el-overlay-1">\n' +
                '                                    <a class="image-popup-vertical-fit" href="#"> <img\n' +
                '                                            src="#"\n' +
                '                                            alt="' + node.data.name + '" style="max-width: 300px"/>\n' +
                '                                    </a>\n' +
                '                                </div>\n' +
                '\n' +
                '                            <div class="table-responsive">\n' +
                '                                <table class="table">\n' +
                '                                    <tbody>\n' +
                '                                    <tr>\n' +
                '                                        <th scope="row">Reg No.</th>\n' +
                '                                        <td>{{ lvl1.reg_no }}</td>\n' +
                '                                    </tr>\n' +
                '                                    <tr>\n' +
                '                                        <th scope="row">Name</th>\n' +
                '                                        <td>' + node.data.name + '</td>\n' +
                '                                    </tr>\n' +
                '\n' +
                '                                    </tbody>\n' +
                '                                </table>\n' +
                '                            </div>\n' +
                '                        </div>\n' +
                '                    </div>\n' +
                '                    <div class="tab-pane p-20" id="bio' + node.id + '" role="tabpanel">2</div>\n' +
                '                    <div class="tab-pane p-20" id="breeder' + node.id + '" role="tabpanel">\n' +
                '                        {% if lvl1.breeder %}\n' +
                '                            <a href="javascript:{document.getElementById(\'lvl1_breeder\').submit()}">\n' +
                '                                <button class="btn btn-info btn-sm btn-block">\n' +
                '                                    {{ lvl1.breeder }}</button>\n' +
                '                            </a>\n' +
                '                        {% endif %}\n' +
                '                    </div>\n' +
                '                    <div class="tab-pane p-20" id="owner' + node.id + '" role="tabpanel">\n' +
                '                        {% if lvl1.current_owner %}\n' +
                '                            <a href="javascript:{document.getElementById(\'lvl1_owner\').submit()}">\n' +
                '                                <button class="btn btn-info btn-sm btn-block">\n' +
                '                                    {{ lvl1.current_owner }}</button>\n' +
                '                            </a>\n' +
                '                        {% endif %}\n' +
                '                    </div>\n' +
                '                </div>\n' +
                '            </div>\n' +
                '        </div>';
            label.onclick = function () {
                if (normal.checked) {
                    st.onClick(node.id);
                } else {
                    st.setRoot(node.id, 'animate');
                }
            };
            //set label styles
            var style = label.style;
            style.cursor = 'pointer';

        },

        //This method is called right before plotting
        //a node. It's useful for changing an individual node
        //style properties before plotting it.
        //The data properties prefixed with a dollar
        //sign will override the global node style properties.
        onBeforePlotNode: function (node) {
            //add some color to the nodes in the path between the
            //root node and the selected node.
            if (node.selected) {
                node.data.$color = "#343a40";
            }
            else {
                delete node.data.$color;
                //if the node belongs to the last plotted level
                if (!node.anySubnode("exist")) {
                    //count children number
                    var count = 0;
                    node.eachSubnode(function (n) {
                        count++;
                    });
                    //assign a node color based on
                    //how many children it has
                    node.data.$color = ['#343a40', '#343a40', '#343a40'][count];
                }
            }
        },

        //This method is called right before plotting
        //an edge. It's useful for changing an individual edge
        //style properties before plotting it.
        //Edge data proprties prefixed with a dollar sign will
        //override the Edge global style properties.
        onBeforePlotLine: function (adj) {
            if (adj.nodeFrom.selected && adj.nodeTo.selected) {
                adj.data.$color = "#eed";
                adj.data.$lineWidth = 3;
            }
            else {
                delete adj.data.$color;
                delete adj.data.$lineWidth;
            }
        }
    });
    //load json data
    st.loadJSON(json);
    //compute node positions and layout
    st.compute();
    //optional: make a translation of the tree
    st.geom.translate(new $jit.Complex(-200, 0), "current");
    //emulate a click on the root node.
    st.onClick(st.root);
    //end
    //Add event handlers to switch spacetree orientation.
    var top = $jit.id('r-top'),
        left = $jit.id('r-left'),
        bottom = $jit.id('r-bottom'),
        right = $jit.id('r-right'),
        normal = $jit.id('s-normal');


    function changeHandler() {
        if (this.checked) {
            top.disabled = bottom.disabled = right.disabled = left.disabled = true;
            st.switchPosition(this.value, "animate", {
                onComplete: function () {
                    top.disabled = bottom.disabled = right.disabled = left.disabled = false;
                }
            });
        }
    };

    top.onchange = left.onchange = bottom.onchange = right.onchange = changeHandler;
    //end

}
