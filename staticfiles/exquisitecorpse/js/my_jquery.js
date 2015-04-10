// Make rows in a table clickable
jQuery(document).ready(function($) {
    $(".clickable-row").click(function() {
        window.document.location = $(this).data("href");
    });
});

// Reload single page element by id
<script type="text/javascript">
    function reload(elementId){
            var container = document.getElementById(elementId);
            var content = container.innerHTML;
            container.innerHTML= content;
        }
</script>