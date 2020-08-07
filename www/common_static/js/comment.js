var update_from = function() {
    // 获取回复输入框父级对象
    const vreply_wrapper = $("#reply-vpanel").parent();

    // 回复表单的默认数据
    $('#parent_id').attr('value', vreply_wrapper.attr('parent-id'));
    $('#reply_id').attr('value', vreply_wrapper.attr('reply-id'));
};

// 获取url全称
$(".redirect_url").attr('value', location.protocol+"//" + location.host + location.pathname);

$(function(){
    //页面加载完毕后开始执行的事件

    // 回复按钮
    $(".reply_btn").click(function(){
        $(this).parent().parent().children('.vreply-wrapper').append($('#reply-vpanel'));
        update_from();  // 更新
        $("#reply-vpanel").css("display", "block");  // 显示回复表单
        $("p.cancel-reply").css("display", "block");  // 显示取消回复按钮
        // $("#comment-vpanel").css("display", "none");  // 隐藏评论表单
    });

    // 取消回复按钮
    $('p.cancel-reply').click(function(){
        update_from();  // 更新表单移动后的数据
        $("#reply-vpanel").css("display", "none");  // 隐藏回复表单
        $("p.cancel-reply").css("display", "none");  // 隐藏取消回复按钮
        // $("#comment-vpanel").css("display", "block");  // 显示评论表单
    });
});

