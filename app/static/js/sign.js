
function ajax_request(method, url, data, async)
{
    var responseText = "";
    var xmlhttp = new XMLHttpRequest();
    //xmlHttp.open("POST","verify_user", false);
    //2.注册回调函数
    //onreadystatechange是每次 readyState 属性改变的时候调用的事件句柄函数。
    xmlhttp.onreadystatechange = callbackfun;
    //3.设置连接信息
      //初始化HTTP请求参数，但是并不发送请求。
      //第一个参数连接方式，第二是url地址,第三个true是异步连接，默认是异步
      xmlhttp.open(method,url,async);
      //使用post方式发送数据
      //xmlhttp.open("POST","http://xxx.php",true);
      //post需要自己设置http的请求头
    xmlhttp.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
    
      //4，发送数据，开始和服务器进行交互
          //发送 HTTP 请求，使用传递给 open() 方法的参数，以及传递给该方法的可选请求体。
          //中如果true, send这句话会立即执行
          //如果是false（同步），send会在服务器数据回来才执行
          
    xmlhttp.send(data);
          //因为是get所以send中不需要内容
          //xmlhttp.send('name=' +username);
    
      //5，回调函数,不同相应状态进行处理
    function callbackfun()
    {
        //alert(xmlhttp.readyState);
        //判断对象状态是交互完成，接收服务器返回的数据
        if (xmlhttp.readyState==4)
        {
            if(xmlhttp.status == 200)
            {
                //纯文本的数据
                responseText = xmlhttp.responseText;
                //alert(responseText + xmlHttp.readyState);
            }
            else
            {
                alert("请求未成功，请检查网络！状态码：" + xmlhttp.status);
                responseText = '{"result":0}';

            }    
        }
    }
    return responseText;
}


function add_class(obj, myClassName) {
    obj.setAttribute("class", obj.className + " " + myClassName);
}

function remove_class(obj, myClassName) {
    class_list = obj.classList;
    var len = class_list.length;
    var new_class = "";
    for(var i = 0; i < len; i++)
    {
        if(class_list[i] != myClassName)
        {
            new_class = new_class + " " + class_list[i];
        }
    }
    obj.setAttribute("class", new_class);
}

function verify_email(inputEmail)
{
    //alert(inputEmail);
    var pattern = "^\\w+@[a-zA-Z0-9]+(\\.[a-z]+){1,3}$";
    var reg = RegExp(pattern);
    var result = inputEmail.match(reg);
    //alert(result);
    if(result == null)
    {
        return false;
    }
    else
    {
        return true;
    }
}

function verify_password(firstPassword, sencondPassword) {
    if(firstPassword == sencondPassword && firstPassword.length >= 8)
    {
        return true;
    }
    else
    {
        return false;
    }
}

function verify_captcha(capt) {
    var re = /^[0-9]{6}$/;
    var result = capt.search(re);
    if(capt.length == 6 && result != -1)
    {
        return true;
    }
    else
    {
        return false;
    }
}

function captcha_onblur(id) {
    var obj = document.getElementById(id);
    var captcha_err_obj = document.getElementById("captcha_feedback");
    if(verify_captcha(obj.value))
    {
        remove_class(obj, "is-valid");
        remove_class(obj, "is-invalid");
        add_class(obj, "is-valid");
        captcha_err_obj.innerHTML = "";

    }
    else
    {
        captcha_err_obj.innerHTML = "请输入六位数字的验证码！";

        remove_class(obj, "is-valid");
        remove_class(obj, "is-invalid");
        add_class(obj, "is-invalid");            
        
    }
}


function signupPassword_onblur(first_id, sencond_id ) {
    var first_obj = document.getElementById(first_id);
    var firstPassword = first_obj.value;
    var sencond_obj = document.getElementById(sencond_id);
    var sencondPassword = sencond_obj.value;
    var parent_node = sencond_obj.parentNode;
    var second_node = document.getElementById("second_feedback");
    second_node.setAttribute("class", "invalid-feedback");

    if(verify_password(firstPassword, sencondPassword))
    {
        remove_class(sencond_obj, "is-valid");
        remove_class(sencond_obj, "is-invalid");
        add_class(sencond_obj, "is-valid");
        remove_class(first_obj, "is-valid");
        remove_class(first_obj, "is-invalid");
        add_class(first_obj, "is-valid");
    }
    else
    {
       
        second_node.innerHTML = "密码至少要八个字符且两次输入一致！";
        remove_class(sencond_obj, "is-valid");
        remove_class(sencond_obj, "is-invalid");
        add_class(sencond_obj, "is-invalid");
        remove_class(first_obj, "is-valid");
        remove_class(first_obj, "is-invalid");
        add_class(first_obj, "is-invalid");
    }
}


function signupEmail_onblur(id) {
    var obj = document.getElementById(id);
    var parent_node = obj.parentNode;

    var node=document.getElementById("email_feedback");
    node.setAttribute("class", "invalid-feedback");
    email = obj.value;
    if(verify_email(email))
    {
        remove_class(obj, "is-valid");
        remove_class(obj, "is-invalid");
        add_class(obj, "is-valid");
        var data = "email=" + email;
        var response = ajax_request("POST","/auth/verifyEmail", data, false);
        var response_obj = JSON.parse(response);
        if(response_obj["result"] != 1)
        {
            remove_class(obj, "is-valid");
            remove_class(obj, "is-invalid");
            add_class(obj, "is-invalid");
            node.innerHTML="该邮箱已经被注册！";   
        }
    }
    else
    {

        node.innerHTML = "请输入正确的邮箱地址！";  
        remove_class(obj, "is-valid");
        remove_class(obj, "is-invalid");
        add_class(obj, "is-invalid");            
        
    }
    
}


function username_onblur(id) {
    var obj = document.getElementById(id);
    var parent_node = obj.parentNode;
    
    var node = document.getElementById("username_feedback") 
    node.setAttribute("class", "invalid-feedback")

    var len = obj.value.length;
    if(len <= 20 && len != 0)
    {
        remove_class(obj, "is-valid");
        remove_class(obj, "is-invalid");
        add_class(obj, "is-valid");
        var data = "username=" + obj.value;
        var response = ajax_request("POST","/auth/verifyUser", data, false);
        var response_obj = JSON.parse(response);
        if(response_obj["result"] != 1)
        {
            remove_class(obj, "is-valid");
            remove_class(obj, "is-invalid");
            add_class(obj, "is-invalid");
            node.innerHTML="用户名已经被使用！";   
        }
        
    }
    else
    {
        
        
        node.innerHTML="用户名少于20个字符或十个汉字且不能为空。";
        remove_class(obj, "is-valid");
        remove_class(obj, "is-invalid");
        add_class(obj, "is-invalid");     
    }   
}
    



function get_captcha(id) {
    var obj = document.getElementById(id);
    var email_obj = document.getElementById("signupEmail");
    if(!verify_email(email_obj.value))
    {
        return false;
    }
    var data = "email=" + email_obj.value;
    var response = ajax_request("POST", "captcha", data, false)
    var response_obj = JSON.parse(response);

    if(response_obj["result"] == 1)
    {
        obj.setAttribute("disabled", "true");
        var clock = '';
        var nums = 60;
        obj.value = nums+'秒后可重新获取';
        clock = setInterval(doLoop, 1000); //一秒执行一次
        function doLoop()
         {
             nums--;
             if(nums > 0)
            {
                obj.textContent = nums+'秒后重新获取';
             }
            else
            {
                clearInterval(clock); //清除js定时器
                obj.disabled = false;
                obj.textContent = '点击发送验证码';
                //nums = 60; //重置时间
            }
         }
        return false;
    }
}

function signin_onclick()
{
    var inputEmail = signin_form.inputEmail.value;
    var inputPassword = signin_form.inputPassword.value;
    var signin_err_obj = document.getElementById("signin_err");
    var data = "inputEmail=" + inputEmail + "&inputPassword=" + inputPassword;
    var response = ajax_request("POST", "/auth/signin", data, false);
    var response_obj = JSON.parse(response)
    if(response_obj["result"] == 1)
    {
        return true;
    }
    else
    {
        signin_err_obj.innerHTML = "邮箱或密码输入错误！";
        signin_err_obj.setAttribute("class", "alert alert-danger");
        return false;
    }
}


function signup_onclick()
{
    captcha = signup_form.captcha.value;
    email = signup_form.signupEmail.value;
    var captcha_err_obj = document.getElementById("captcha_feedback");
    var data = "captcha=" + captcha + "&email=" + email;
    var response = ajax_request("POST", "/auth/verifyCaptcha", data, false);
    var response_obj = JSON.parse(response)
    if(response_obj["result"] == 1)
    {
        return true;
    }
    else
    {
        captcha_err_obj.innerHTML = "请输入正确的验证码！";
        return false;
    }
}

