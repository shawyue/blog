
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

function resetPassword_onclick()
{
    
    var path_name = window.location.pathname;
    var name_list = path_name.split("/");
    var key = name_list[name_list.length-1];
    password = resetPassword_form.firstPassword.value;
    data = "key=" + key + "&password=" + password;
    var response = ajax_request("POST", "/auth/resetPassword/save", data, false);
    var response_obj = JSON.parse(response)
    if(response_obj["result"] == 1)
    {
        document.resetPassword_form.action = response_obj["url"];
        return true;
    }
    else
    {
        captcha_err_obj.innerHTML = "请输入正确的验证码！";
        return false;
    }
}

