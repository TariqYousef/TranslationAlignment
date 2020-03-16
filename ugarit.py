from IPython.core.display import display, HTML
from collections import defaultdict


class Ugarit:
    unique_id = 0

    def __init__(self):
        html = """
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
        <script>
        $(document).on('mouseover', "span[data-ref^='ref_']", function(e) {
            var ref = document.getElementById(e.target.id).getAttribute('data-ref');
            console.log(e.target.id);
            console.log(ref);
            var cls = document.getElementById(e.target.id).getAttribute('class');
            if(cls=="aligned"){
                $("span[data-ref='"+ref+"']").each(function(index){
                    $(this).addClass("highlighted ");
                });
            }
        });
        $(document).on('mouseout', "span[data-ref^='ref_']", function(e) {
            var ref = document.getElementById(e.target.id).getAttribute('data-ref');
            var cls = document.getElementById(e.target.id).getAttribute('class');
            if(cls=="aligned highlighted") {
                $("span[data-ref='" + ref + "']").each(function (index) {
                    $(this).removeClass("highlighted ");
                });
            }
        });
        </script>
        <style>
            .aligned{ color: #5cb85c; 
                     background-color:
                     #FFFFFF; 
                     padding: 2px;}

            .highlighted{
                cursor: pointer; 
                background-color:#c65353; 
                color:#FFFFFF;; 
                padding: 2px; 
                border-radius: 5px; }

            .alignment{
                border-radius: 5px;
                border:1px solid #ccc; 
                padding: 10px; 
            }
            </style>"""
        display(HTML(html))

    def createSpan(self, word, idd, ref):
        cls = "aligned" if ref != "" else ""
        prefix = "al" + str(self.unique_id) + "_"
        return "<span id=\"" + prefix + idd + "\" data-ref=\"" + ref + prefix + "\" class=\"" + cls + "\" >" + word + "</span>"

    def createRef(self, als):
        s1 = defaultdict(list)
        s2 = defaultdict(list)
        cls1 = defaultdict(lambda: "")
        cls2 = defaultdict(lambda: "")
        for a in als.alignment:
            # print(a)
            s1[a[0]].append(a[1])
            s2[a[1]].append(a[0])
        ref = 0

        for id_sent1, alignedTo_sent2 in s1.items():
            if cls1[id_sent1] == "":
                cls1[id_sent1] = "ref_" + str(ref)
                for id_sent2 in alignedTo_sent2:
                    cls2[id_sent2] = "ref_" + str(ref)
                    for i_1 in s2[id_sent2]:
                        if cls1[i_1] == "":
                            cls1[i_1] = "ref_" + str(ref)
            ref += 1
        return {'sent1': cls1, 'sent2': cls2}

    def render(self, als):
        self.unique_id += 1
        cls = self.createRef(als)
        div1 = " ".join([self.createSpan(w, "s1_" + str(i), cls['sent1'][i]) for i, w in enumerate(als.words)])
        div2 = " ".join([self.createSpan(w, "al" + str(self.unique_id) + "_s2_" + str(i), cls['sent2'][i]) for i, w in
                         enumerate(als.mots)])
        display(HTML('<div class="row alignment">' +
                     '<div class="col-md-5">' + div1 +
                     '</div><div class="col-md-2">' +
                     '</div><div class="col-md-5">' + div2 + '</div>' +
                     '</div>'))
