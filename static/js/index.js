(function () {
    var Message;
    Message = function (arg) {
        this.text = arg.text, this.message_side = arg.message_side;
        this.draw = function (_this) {
            return function () {
                var $message;
                $message = $($('.message_template').clone().html());
                $message.addClass(_this.message_side).find('.text').html(_this.text);
                $('.messages').append($message);
                return setTimeout(function () {
                    return $message.addClass('appeared');
                }, 0);
            };
        }(this);
        return this;
    };
    $(function () {
        var getMessageText, sendMessage;
        getMessageText = function () {
            var $message_input;
            $message_input = $('.message_input');
            return $message_input.val();
        };
        sendMessage = function (text) {

            var alert = document.getElementById("alert");
            if (text.trim() === '') {
                alert.innerHTML = "Please enter a message";
                alert.style.color = "red";
                return;
            }
            alert.innerHTML = "";

            $.post('/send_message', { message: text });

            $('.message_input').val('');

            var $messages, message;
            $messages = $('.messages');
            message = new Message({
                text: text,
                message_side: 'right'
            });
            message.draw();
            return $messages.animate({ scrollTop: $messages.prop('scrollHeight') }, 300);
        };
        $('.send_message').click(function (e) {
            return sendMessage(getMessageText());
        });
        $('.message_input').keyup(function (e) {
            if (e.which === 13) {
                return sendMessage(getMessageText());
            }
        });

         // Receive a message and add it to the chat window
         var source = new EventSource('/receive_messages');
         source.onmessage = function(e) {

            var $messages, message;
            $messages = $('.messages');
            message = new Message({
                text: e.data,
                message_side: 'left'
            });
            message.draw();
            $messages.animate({ scrollTop: $messages.prop('scrollHeight') }, 300);

         };

    });
}.call(this));