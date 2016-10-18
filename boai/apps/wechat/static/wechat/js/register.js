/**
 * Created by LBI on 2016/10/18.
 */

var formSubmit = Nature.FormSubmit;

ajaxInfo = {
    url: "/wechat/register/", //ajax请求url
    success_redirect_url: "/wechat/main/" //请求成功跳转url
}

formSubmit({
        rules: {
            mobile: {
                required: true,
                isMobile: true
            },
        },
        messages: {
            mobile: {
                required: "请填写您的手机号码",
                isMobile: "请填写正确的手机号码",
            },
        },
    },
    ajaxInfo
)