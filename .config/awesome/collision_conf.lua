local beautiful = require("beautiful")

beautiful.collision_resize_width = 25
beautiful.collision_resize_shape = shape.circle
--beautiful.collision_resize_border_width
--beautiful.collision_resize_border_color
beautiful.collision_resize_padding = 4
beautiful.collision_resize_bg = "#ff0000"
beautiful.collision_resize_fg = "#0000ff"
require("collision")()
