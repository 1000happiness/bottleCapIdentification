import AccountFetch from "../../public_service/account/AccountFetch";
var EventEmitter = require("events").EventEmitter;
var assign = require("object-assign");

const tabBar = {
    "账户系统-/customer_service/account" : {
        "我的账户" : "/customer_service/account/myaccount",
    },
    "客服系统-/customer_service/message" : {
        "消费者消息" : "/customer_service/message/consumermessage",
    }
}

var CustomerServiceStore = assign({}, EventEmitter.prototype,{
    items : {
        tabBar : null,
        account: null,
        content : null,
    },

    emitChange: function () {
        this.emit("change");
    },
    
    addChangeListener: function(callback) {
        this.on("change", callback);
    },
    
    removeChangeListener: function(callback) {
        this.removeListener("change", callback);
    },

    getItems: function(){
        return this.items;
    },

    init(){
        this.items.tabBar = tabBar;
        this.initAccount();
        this.parseContent();
    },

    initAccount(){
        this.items.account = {
            userId: 1,
            username: "hahaha",
            userRole: "customerService",
        }

        var response = AccountFetch.fetchGetSelfUserInfo(this.items.account.userRole);
        var t=this;
        response.then(function(response){
            console.log(response);
            if(response.status !== 200){
                console.log("存在一个问题，状态码为：" + response.status);
                window.location.href = AccountFetch.getHomeUrl();
                return;
            }
            return response.json();
        }).then(function(data){
            if(data.success){
                t.items.account["userId"] = data.user.id;
                t.items.account["username"] = data.user.username;
                t.emitChange();
                return;
            }
            else{
                console.log(data.errorMassage);
                return;
            }
        }).catch(function(err){
            console.log("获取用户信息失败");
            console.log(err);
        });
    },

    flush(){
        this.initAccount();
        var temp =window.location.href;
        window.location.href = temp;
    },

    parseContent(){
        var sublocalhref = "localhost:3000";
        var href = window.location.href;
        var content = "";
        var temp = "";

        while((temp = href.slice(href.lastIndexOf('/') + 1)) !== sublocalhref) {
            content = "/" + temp + content;
            href = href.slice(0,href.lastIndexOf('/'));
        }

        this.items.content = content;
    }
});

export default CustomerServiceStore;