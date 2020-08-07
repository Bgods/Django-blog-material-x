$(document).ready(function() {
    // 生成目录
    $("#article_content").children().each(function(index, element) {
        var tagName=$(this).get(0).tagName;
        if(tagName.substr(0,1).toUpperCase() === "H"){
            let arr = ['1', '2', '3', '4', '5', '6'];
            if (arr.indexOf(tagName.substr(1,1)) !== -1){
                let contentH=$(this).html().replace(/<[^>]+>/g,"");  // 获取内容
                let toc_id="toc" + index.toString();
                $(this).attr("id", toc_id);  // 为当前h标签设置id
                $(".toc").append("<li><a href='#" + toc_id + "'>" + contentH + "</a></li>");  // 在目标DIV中添加内容
            }
        }
    });

    // 展开和隐藏目录
    $('.toc-show-hide').click(function(){
        $('#toc-content').toggle('slow');
        let toc_icon = $("#toc-icon").attr("class");  // 获取class属性值
        if (toc_icon === 'fas fa-caret-right fa-fw'){
            $('#toc-icon').attr("class","fas fa-caret-down fa-fw");
        } else {
            $('#toc-icon').attr("class","fas fa-caret-right fa-fw");
        }
    });

    // 展开和隐藏
    $('.h2-show-hide').click(function(){
        $(this).next().toggle('slow');
        let toc_icon = $(this).children("i").attr("class");  // 获取class属性值
        if (toc_icon === 'fas fa-caret-right fa-fw'){
            $(this).children("i").attr('class', 'fas fa-caret-down fa-fw');
        } else {
            $(this).children("i").attr('class', 'fas fa-caret-right fa-fw');
        }
    });

});


