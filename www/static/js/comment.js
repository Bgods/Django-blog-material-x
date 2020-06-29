const update_from = function() {
    // 获取回复输入框父级对象
    const vreply_wrapper = document.getElementById("comment-vpanel").parentNode;
    // 获取属性值：parent-id、reply-id
    const parent_id= vreply_wrapper.getAttribute('parent-id');
    const reply_id = vreply_wrapper.getAttribute('reply-id');
    const redirect_url = vreply_wrapper.getAttribute('redirect-url');

    // 更新input标签的值
    document.getElementById('parent_id').setAttribute('value', parent_id);
    document.getElementById('reply_id').setAttribute('value', reply_id);
    document.getElementById('redirect_url').setAttribute('value', location.pathname + redirect_url);
};

const vcards = document.querySelectorAll('div.vcard');
for (let v in vcards){
    const vcard =vcards[v];

    const vat = vcard.querySelector('span.vat'); // 回复按钮

    // 点击回复按钮回调函数
    vat.onclick = function () {
        const vpanel = document.getElementById("comment-vpanel");  //获取回复输入框元素
        vat.parentNode.parentNode.querySelector('div.vreply-wrapper').appendChild(vpanel);  // 移动元素对象到vreply_wrapper对象内
        update_from();  // 更新表单移动后的数据

        const cancel_reply = document.querySelector('p.cancel-reply');  // 获取取消回复按钮对象
        cancel_reply.style.display = 'block';  // 显示取消回复按钮

        // 点击取消按钮回调函数
        cancel_reply.onclick = function (){
            const comments_post = document.getElementById('comments-post');
            comments_post.appendChild(vpanel);
            update_from();  // 更新表单移动后的数据
            cancel_reply.style.display = 'none';  // 隐藏取消回复按钮
        };
    };
}
