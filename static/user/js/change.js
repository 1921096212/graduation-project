$(function () {

    $("#btn1").click(function () {
        $.ajax({
            url: "/change/",
            type: "PUT",
            data: JSON.stringify({"username":$("#inp1").val()}),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
        })
            .done(function (res) {
                alert(res.msg);
            })
            .fail(function () {
                alert('服务器超时，请重试！');
            });

    });


});