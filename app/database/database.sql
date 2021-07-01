
--postgresql 10

DROP TABLE IF EXISTS applied_filter;

DROP TABLE IF EXISTS picture;

DROP TABLE IF EXISTS users;

DROP TABLE IF EXISTS filter;

create table users (
    id integer primary key,
    email varchar(255),
    first_name varchar(255), 
    last_name varchar(255), 
    password varchar(255)
);

create table picture (
    id integer primary key,
    created_date timestamp,
    img bytea,
    name varchar(255),
    updated_date timestamp,
    user_id int8 not null references users(user_id)
);

-- alter table picture add constraint FKsm5vfwexx74npg3319l47fhdi foreign key (user_id) references users;

create table applied_filter (id int8 not null, date timestamp, filter_id int8 not null, picture_id int8 not null, primary key (id));

create table filter (
    id integer primary key not null, 
    description text, 
    is_linear boolean, 
    name varchar(255)
);


insert into filter(name, is_linear, description) values('box_filter', true, 'A box blur (also known as a box linear filter) is a spatial domain linear filter in which each pixel in the resulting image has a value equal to the average value of its neighboring pixels in the input image.\n It is a form of low-pass ("blurring") filter. Due to its property of using equal weights, it can be implemented using a much simpler accumulation algorithm, which is significantly faster than using a sliding-window algorithm. In the frequency domain, a box blur has zeros and negative components.\n That is, a sine wave with a period equal to the size of the box will be blurred away entirely, and wavelengths shorter than the size of the box may be phase-reversed, as seen when two bokeh circles touch to form a bright spot where there would be a dark spot between two bright spots in the original image.\n');
insert into filter(name, is_linear, description) values('gussian_filter', true, 'In image processing, a Gaussian blur (also known as Gaussian smoothing) is the result of blurring an image by a Gaussian function (named after mathematician and scientist Carl Friedrich Gauss).\n It is a widely used effect in graphics software, typically to reduce image noise and reduce detail. The visual effect of this blurring technique is a smooth blur resembling that of viewing the image through a translucent screen, distinctly different from the bokeh effect produced by an out-of-focus lens or the shadow of an object under usual illumination.\nGaussian smoothing is also used as a pre-processing stage in computer vision algorithms in order to enhance image structures at different scales—see scale space representation and scale space implementation.');
insert into filter(name, is_linear, description) values('bilateral_filter', false, 'A bilateral filter is a non-linear, edge-preserving, and noise-reducing smoothing filter for images. It replaces the intensity of each pixel with a weighted average of intensity values from nearby pixels. This weight can be based on a Gaussian distribution. Crucially, the weights depend not only on Euclidean distance of pixels, but also on the radiometric differences (e.g., range differences, such as color intensity, depth distance, etc.). This preserves sharp edges.\n As the range parameter σr increases, the bilateral filter gradually approaches Gaussian convolution more closely because the range Gaussian widens and flattens, which means that it becomes nearly constant over the intensity interval of the image. As the spatial parameter σd increases, the larger features get smoothened.');
-- alter table applied_filter add constraint FK5es6qwhmkmgs10kpjika3klum foreign key (filter_id) references filter;
-- alter table applied_filter add constraint FK9nvi5qabomlnpa7c9hg1jpqip foreign key (picture_id) references picture;
