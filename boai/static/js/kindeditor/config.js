/**
 * Created by v_biaoliu on 2016/12/19.
 */


//config.js
KindEditor.ready(function (K) {
    window.editor = K.create('#id_remark', {

        // 指定大小
        width: '800px',
        height: '200px',

        allowPreviewEmoticons: false,
        <!--去掉远程上传的功能-->
        allowImageRemote: false,
        <!--后台处理上传图片的功url-->
        uploadJson: '/wechat/uploadimg/',
        // items: [
        //     'fontname', 'fontsize', '|', 'forecolor', 'hilitecolor', 'bold', 'italic', 'underline',
        //     'removeformat', '|', 'justifyleft', 'justifycenter', 'justifyright', 'insertorderedlist',
        //     'insertunorderedlist', '|', 'emoticons', 'image', 'link']
    });
});