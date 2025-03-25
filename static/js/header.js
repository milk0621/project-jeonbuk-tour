// 폰트
(function(d) {
    var config = {
    kitId: 'ses4qhw',
    scriptTimeout: 3000,
    async: true
    },
    h=d.documentElement,t=setTimeout(function(){h.className=h.className.replace(/\bwf-loading\b/g,"")+" wf-inactive";},config.scriptTimeout),tk=d.createElement("script"),f=false,s=d.getElementsByTagName("script")[0],a;h.className+=" wf-loading";tk.src='https://use.typekit.net/'+config.kitId+'.js';tk.async=true;tk.onload=tk.onreadystatechange=function(){a=this.readyState;if(f||a&&a!="complete"&&a!="loaded")return;f=true;clearTimeout(t);try{Typekit.load(config)}catch(e){}};s.parentNode.insertBefore(tk,s)
})(document);

//로그인
$(document).ready(function() {
    $("#login-btn").click(function() {
        $("#login-modal").fadeIn();
    });

    $(".close").click(function() {
        $("#login-modal").fadeOut();
    });

    $(window).click(function(event) {
        if ($(event.target).is("#login-modal")) {
            $("#login-modal").fadeOut();
        }
    });
});

//회원가입 -> 로그인
$(document).ready(function() {
    $("#login").click(function() {
        $("#join-modal").fadeOut();
        $("#login-modal").fadeIn();
    });

    $(".close").click(function() {
        $("#login-modal").fadeOut();
    });

    $(window).click(function(event) {
        if ($(event.target).is("#login-modal")) {
            $("#login-modal").fadeOut();
        }
    });
});

//회원가입
$(document).ready(function() {
    $("#join").click(function() {
        $("#join-modal").fadeIn();
    });

    $(".close").click(function() {
        $("#join-modal").fadeOut();
    });

    $(window).click(function(event) {
        if ($(event.target).is("#join-modal")) {
            $("#join-modal").fadeOut();
        }
    });
});