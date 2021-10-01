tinymce.init({
  selector: "textarea",
  browser_spellcheck: true,
  contextmenu: false,
  toolbar_sticky: true,
  autosave_ask_before_unload: true,
  autosave_interval: "30s",
  autosave_prefix: "{path}{query}-{id}-",
  autosave_restore_when_empty: false,
  autosave_retention: "2m",
  default_link_target: "_blank",
  menubar: "file edit view insert format tools table",
  toolbar: "undo redo | code visualblocks preview fullscreen | link image paste | template save",
  plugins: "code visualblocks preview fullscreen template paste searchreplace link autolink image anchor toc lists table autosave save"
});