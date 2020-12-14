// Close contract
$(function () {
  $("a#close_contract").bind("click", function () {
    $.ajax({
      url: "/exchange/close",
      type: "POST",
      data: {
        contractId: $('input[name="contract"]').val(),
        action: "close",
      },
      dataType: "json",
      success: function (data) {
        $("#contract-section").load(" #contract-section > *");
      },
    });
    return false;
  });
});
