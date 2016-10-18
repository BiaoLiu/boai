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
                isMobile: true
            },
            password2: {
                equalTo: '#password'
            }
        },
        messages: {
            mobile: {
                isMobile: "请填写正确的手机号码"
            },
            password2: {
                equalTo: "两次密码不一致"
            }
        },
    },
    ajaxInfo
)