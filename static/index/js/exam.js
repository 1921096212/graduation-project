$(function () {
    // 缓存题目
    var content = '';
    // 标志位
    var x = 0;
    // 成绩
    var marks = 0;
    // 成绩列表
    var list_marks = [];
    // 当前难度id
    var sCurrentTagId = 0;
    // 隐藏提交按钮
    $("#but2").toggle();

    //1.向服务器请求题目并显示
    $(".list-group-item").click(function () {
        // 获取这个标签的的属性
        sCurrentTagId = $(this).attr('data-id');
        $.ajax({
            url: "/exam/?p=" + sCurrentTagId,
            type: "GET",
            dataType: "json",
        })
            .done(function (res) {
                // 缓存数据
                content = res;
                // 1.1隐藏按钮
                $("#ul1").toggle();
                // 1.2给考试div赋值
                $("#title").text(res.data[x].title);
                $("#optionsRadios1").text(res.data[x].A);
                $("#optionsRadios2").text(res.data[x].B);
                $("#optionsRadios3").text(res.data[x].C);
                $("#optionsRadios4").text(res.data[x].D);
                // 1.3显示考试div
                $("#div2").toggle();
            })
            .fail(function () {
                alert('服务器超时，请重试！');
            });
    });
    //2.切换题目
    $("#but1").click(function () {
        // 更新成绩
        var checked_v = $("input[name='optionsRadios']:checked").val();
        // 过滤未选中状态
        if (checked_v === undefined) {
            alert('请选择答案!');
        } else {
            if (content.data[x].wor == checked_v) {
                marks = marks + 10;
                list_marks[x] = 1
            } else {
                list_marks[x] = 0
            }
            x = x + 1;
            // alert(content.data[x].wor);
            $("#title").text(content.data[x].title);
            $("#optionsRadios1").text(content.data[x].A);
            $("#optionsRadios2").text(content.data[x].B);
            $("#optionsRadios3").text(content.data[x].C);
            $("#optionsRadios4").text(content.data[x].D);
            $("#s").text('第' + x + '题/共10题');
            // 如果到最后一道题时显示提交按钮
            if (x == content.data.length-1) {
                $("#but1").toggle();
                $("#but2").toggle();
            }
        }

    });
    //3.答完上传成绩
    $("#but2").click(function () {
        // 创建请求参数
        let mark = {
            "level": sCurrentTagId,
            "marks": marks
        };
        $.ajax({
            url: "/exam/",
            type: "POST",
            data: JSON.stringify(mark),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
        })
            .done(function (res) {
                var mark_c = '';
                var str_marks = '';
                // 刷新学生信息界面
                $("#div2").toggle();
                $("#mark").text(marks + '分');
                for (var i = 0; i < content.data.length; i++) {
                    str_marks = '第' + (i+1) + '题';
                    if (list_marks[i] === 1) {
                        mark_c = `<div class="col-md-2" style="background-color: #6DB46D;padding: 10px;box-shadow:inset 1px -1px 1px #ffffff, inset -1px 1px 1px #ffffff;">
                            <p>${str_marks}</p>
                            </div>`;
                    } else {
                        mark_c = `<div class="col-md-2" style="background-color: #FF9191;padding: 10px;box-shadow:inset 1px -1px 1px #ffffff, inset -1px 1px 1px #ffffff;">
                            <p>${str_marks}</p>
                            </div>`;
                    }
                    $("#col").append(mark_c);
                }
                $("#div3").toggle();
            })
            .fail(function () {
                alert('服务器超时，请重试！');
            });
    });

});