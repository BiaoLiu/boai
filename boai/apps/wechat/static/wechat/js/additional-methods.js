/**
 * Created by LBI on 2016/10/18.
 */

//验证11位手机号码
jQuery.validator.addMethod('isMobile', function (value, element) {
    return this.optional(element) || checkIsMobile(value);
}, '手机格式不正确');
//验证纯数字60位以为
jQuery.validator.addMethod('checkNum', function (value, element) {
    return this.optional(element) || /[0-9]{1,60}$/.test(value);
}, '手机格式不正确');

//验证11位手机号码
jQuery.validator.addMethod('isUserName', function (value, element) {
    return this.optional(element) || /[a-zA-Z0-9_]{6,16}$/i.test(value);
}, 'Please specify a valid Mobile');

//验证邮编
jQuery.validator.addMethod('isPostCode', function (value) {
    return checkPostCode(value);
}, '输入正确的邮编');

//ajax验证手机号码是否被占用
jQuery.validator.addMethod("isMobileExist", function (value, element) {
    var flag = false;
    $.ajax({
        type: "POST",
        url: "/users/checkMobileAjax/",
        data: "mobile=" + value,
        async: false,
        dataType: "json",
        success: function (data) {
            //alert("返回数据: " + msg);
            if (data.status == '1') {
                flag = true;
            }
        }
    });
    return this.optional(element) || flag;//非必填项目时可以通过
});
//邮箱格式
jQuery.validator.addMethod('isEmail', function (value, element) {
    return this.optional(element) || /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/i.test(value);
}, 'Please specify a valid Email');

//ajax验证邮箱是否被占用
jQuery.validator.addMethod("isEmailExist", function (value, element) {
    var flag = false;
    var id = $("#isEmailExist").val();
    $.ajax({
        type: "POST",
        url: "/ajax/yg/checkEmail.php",
        data: "email=" + value + "&yg_id=" + id,
        async: false,
        dataType: "json",
        success: function (data) {
            //alert("返回数据: " + msg);
            if (data.status == '1') {
                flag = true;
            }
        }
    });
    return this.optional(element) || flag;//非必填项目时可以通过
});
//身份证
jQuery.validator.addMethod("isCard", function (value, element) {
    var flag = isIdCardNo(value);
    return this.optional(element) || flag;
}, "请正确输入您的身份证号码");
//校验特殊字符和数字（包含返回 false）;
jQuery.validator.addMethod("checkSpecialAndNum", function (value, element) {
    var flag = checkSpecialAndNum(value);
    return this.optional(element) || !flag;
}, "输入内容不能存在特殊字符或者数字");
//校验是否包含特殊字符(包含特殊字符返回false)
jQuery.validator.addMethod("checkSpecial", function (value, element) {
    var flag = checkSpecial(value);
    return this.optional(element) || !flag;
}, "输入内容不能存在特殊字符");

//校验名字
jQuery.validator.addMethod("checkName", function (value, element) {
    var flag = checkName(value);
    var en_flag = checkEnName(value);
    return this.optional(element) || flag || en_flag;
}, "输入名称格式不正确");

jQuery.validator.addMethod("requiredOne", function (value, element) {
    // check if dependency is met
    if ($("input[name=is_social]:checked").val() == 1) {
        return requiredCheck(value, element);
    }
    return true;
}, "必须填写");
jQuery.validator.addMethod("isTypeRequired", function (value, element) {
    // check if dependency is met
    if ($(".fl_type").val() == 5) {
        return $.trim(value).length > 0
    }
    return true;
}, "必须填写");
//邮箱或者手机号
jQuery.validator.addMethod("isExitName", function (value, element) {
    if (checkIsMobile(value) || checkIsEmail(value)) {
        return true;
    }
    else {
        return false;
    }
}, "必须填写");

//用户名是否存在
jQuery.validator.addMethod("isRequerName", function (value, element) {
    var flag = false;
    $.ajax({
        type: "POST",
        url: "/ajax/login/checkUsername.php",
        data: "username=" + value,
        async: false,
        dataType: "json",
        success: function (data) {
            if (data.status == 1) {
                flag = true;
            }
        }
    });
    return flag;//非必填项目时可以通过
}, "必须填写");


//验证非空
function requiredCheck(value, element) {
    switch (element.nodeName.toLowerCase()) {
        case 'select':
            // could be an array for select-multiple or a string, both are fine this way
            var val = $(element).val();
            return val && val.length > 0;
        case 'input':
            if ((/radio|checkbox/i).test(element.type))
                return this.getLength(value, element) > 0;
        default:
            return $.trim(value).length > 0;
    }
}

//验证邮件格式
function checkIsEmail(email) {
    return /^[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$/i.test(email);
}
//手机号码格式
function checkIsMobile(mobile) {
    return /^(((13[0-9]{1})|(15[0-3]{1})|(15[5-9]{1})|(145)|(147)|(17[0-9]{1})|(18[0-9]{1}))+\d{8})$/i.test(mobile);
}
//是否为空
function checkIsRequired(str) {
    if (!str || typeof(str) == "undefined" || str == "") {
        return false;
    }
    else {
        return true;
    }
}
function isIdCardNo(value) {
    var flag = false;
    var Wi = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2, 1];    // 加权因子
    var ValideCode = [1, 0, 10, 9, 8, 7, 6, 5, 4, 3, 2];            // 身份证验证位值.10代表X
    var idCard = trim(value.replace(/ /g, ""));               //去掉字符串头尾空格
    if (idCard.length == 15) {
        flag = isValidityBrithBy15IdCard(idCard);       //进行15位身份证的验证
    }
    else if (idCard.length == 18) {
        var a_idCard = idCard.split("");                // 得到身份证数组
        if (isValidityBrithBy18IdCard(idCard) && isTrueValidateCodeBy18IdCard(a_idCard)) {   //进行18位身份证的基本验证和第18位的验证
            flag = true;
        }
    }
    return flag;
}

function isDate6(sDate) {
    if (!/^[0-9]{6}$/.test(sDate)) {
        return false;
    }
    var year, month, day;
    year = sDate.substring(0, 4);
    month = sDate.substring(4, 6);
    if (year < 1700 || year > 2500) return false
    if (month < 1 || month > 12) return false
    return true
}
function isDate8(sDate) {
    if (!/^[0-9]{8}$/.test(sDate)) {
        return false;
    }
    var year, month, day;
    year = sDate.substring(0, 4);
    month = sDate.substring(4, 6);
    day = sDate.substring(6, 8);
    var iaMonthDays = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if (year < 1700 || year > 2500) return false
    if (((year % 4 == 0) && (year % 100 != 0)) || (year % 400 == 0)) iaMonthDays[1] = 29;
    if (month < 1 || month > 12) return false
    if (day < 1 || day > iaMonthDays[month - 1]) return false
    return true
}

/**
 * 判断身份证号码为18位时最后的验证位是否正确
 * @param a_idCard 身份证号码数组
 * @return
 */
function isTrueValidateCodeBy18IdCard(a_idCard) {
    var Wi = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2, 1];    // 加权因子
    var ValideCode = [1, 0, 10, 9, 8, 7, 6, 5, 4, 3, 2];            // 身份证验证位值.10代表X
    var sum = 0;                             // 声明加权求和变量
    if (a_idCard[17].toLowerCase() == 'x') {
        a_idCard[17] = 10;                    // 将最后位为x的验证码替换为10方便后续操作
    }
    for (var i = 0; i < 17; i++) {
        sum += Wi[i] * a_idCard[i];            // 加权求和
    }
    valCodePosition = sum % 11;                // 得到验证码所位置
    if (a_idCard[17] == ValideCode[valCodePosition]) {
        return true;
    } else {
        return false;
    }
}
/**
 * 验证18位数身份证号码中的生日是否是有效生日
 * @param idCard 18位书身份证字符串
 * @return
 */
function isValidityBrithBy18IdCard(idCard18) {
    var year = idCard18.substring(6, 10);
    var month = idCard18.substring(10, 12);
    var day = idCard18.substring(12, 14);
    var temp_date = new Date(year, parseFloat(month) - 1, parseFloat(day));
    // 这里用getFullYear()获取年份，避免千年虫问题
    if (temp_date.getFullYear() != parseFloat(year)
        || temp_date.getMonth() != parseFloat(month) - 1
        || temp_date.getDate() != parseFloat(day)) {
        return false;
    } else {
        return true;
    }
}
/**
 * 验证15位数身份证号码中的生日是否是有效生日
 * @param idCard15 15位书身份证字符串
 * @return
 */
function isValidityBrithBy15IdCard(idCard15) {
    var year = idCard15.substring(6, 8);
    var month = idCard15.substring(8, 10);
    var day = idCard15.substring(10, 12);
    var temp_date = new Date(year, parseFloat(month) - 1, parseFloat(day));
    // 对于老身份证中的你年龄则不需考虑千年虫问题而使用getYear()方法
    if (temp_date.getYear() != parseFloat(year)
        || temp_date.getMonth() != parseFloat(month) - 1
        || temp_date.getDate() != parseFloat(day)) {
        return false;
    } else {
        return true;
    }
}
//去掉字符串头尾空格
function trim(str) {
    return str.replace(/(^\s*)|(\s*$)/g, "");
}
//验证金额(小数点两位)
function isSalary(a){
    var reg = /^[0-9]+([.]{1}[0-9]{1,2})?$/;
    return reg.test(a);
}
//校验银行账号，数字12-19位
function isBankNum(str){
	var reg = /^[0-9]{12,20}?$/;
	return reg.test(str);
}
//校验名字
function checkName(value){
    var reg = /^[\u4e00-\u9fa5a-z]+$/gi;
    return reg.test(value);
}
//校验名字
function checkEnName(value){
    var reg = /^[a-z ']+$/gi;
    return reg.test(value);
}
//校验电话号码(只校验数字或者数字+‘-’位数7-12位)
function checkIsPhone(value){
    var reg = /^[0-9\-]{7,13}?$/;
    return reg.test(value);
}
//校验特殊字符
function checkSpecial(value){
    var reg = /[\'.,:;*?~`!@#$%^&+=<>{}]|\]|\[|\/|\\\|\"|\|/;
    return reg.test(value);
}
//校验特殊字符和数字
function checkSpecialAndNum(value){
    var reg = /[\'.,:;*?~`!@#$%^&+=<>{}0-9]|\]|\[|\/|\\\|\"|\|/;
    return reg.test(value);
}
//校验邮编，数字6位
function checkPostCode(str){
	var reg = /^\d{6}$/;
	return reg.test(str);
}