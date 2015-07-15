(function($) {

  'use strict';

  /* Bloodhound base scripts */

  $.bloodhound = {

    /* General application initialization */

    init: function () {

    }

  };

  $(".js-jump-page").popover({
    html: true,
    content: function () {
      var first_page = "?page=1";
      var last_page_number = $("#products").attr("data-num-pages");
      var last_page = "?page=" + last_page_number;

      var querystring = $("[name='q']").val();
      if (querystring.length > 0) {
        first_page += "&q=" + querystring;
        last_page += "&q=" + querystring;
      }

      var order = $("[name='o']").val();
      if (order.length > 0) {
        first_page += "&o=" + order;
        last_page += "&o=" + order;
      }

      var html = "<div><small><a href='" + first_page + "'>First page</a></small></div>";
      html += "<div><small><a href='" + last_page + "'>Last page</a></small></div>";
      return html;
    }
  });

})(jQuery);
