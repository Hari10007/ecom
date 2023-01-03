
$(document).ready(function(){
    $('#rzp-button1').click(function(e) {
        e.preventDefault();
        var id = $("[name='address']").val();
        var token =$("[name='csrfmiddlewaretoken']").val();
        data = {
            "address": id,
        }
        $.ajax({
            method: "GET",
            url: "/proceed-to-pay",
            data: data,
            success: function (response) {
                var options = {
                    "key": "rzp_test_vaG6opnGOk3U22", // Enter the Key ID generated from the Dashboard
                    "amount": response.order.amount, // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
                    "currency": "INR",
                    "name": "Fashion Hub",
                    "description": "Thank You for buying from us.",
                    "image": "https://example.com/your_logo",
                    "order_id": response.order.id,
                    "handler": function (responses){
                        data = {
                          "payment_method": "Paid by RazorPay",
                          "address": id,
                          "transaction_id": responses.razorpay_payment_id,
                           csrfmiddlewaretoken: token,
                        }
                        $.ajax({
                            method: "POST",
                            url: "/place_order",
                            data: data,
                            //
                            success: function (response) {
                                swal("Congratulations!",response.status,"success").then((value) => {
                                    window.location.href="/order/thank_you"
                                });
                            }
                        });
                    },
                    "prefill": {
                        "name": response.f_name+" "+response.l_name,
                        "email": response.email,
                        "contact": response.ph_no
                    },
                    "notes": {
                        "address": response.address
                    },
                    "theme": {
                        "color": "#3399cc"
                    }
                };
                var rzp1 = new Razorpay(options);
                rzp1.open();
            }
        });
        
        
    })
})