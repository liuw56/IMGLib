CREATE DATABASE  IF NOT EXISTS `img_repo` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `img_repo`;


DROP TABLE IF EXISTS `inventory`;
create table `inventory` (
	`inventory_id` int(11) NOT NULL,
    primary key (`inventory_id`)
);

DROP TABLE IF EXISTS `cart`;
create table `cart` (
	`cart_id` int(11) NOT NULL,
    primary key (`cart_id`)
);

DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `user_id` int(11) NOT NULL,
  `first_name` varchar(45) DEFAULT NULL,
  `last_name` varchar(45) DEFAULT NULL,
  `inventory_id` int(11) DEFAULT NULL,
  `cart_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  foreign key (`inventory_id`) references inventory(`inventory_id`),
  foreign key (`cart_id`) references cart(`cart_id`)
);

DROP TABLE IF EXISTS `item`;
create table `item` (
    `item_id` int(11) NOT NULL,
    `item_name` varchar(45) NOT NULL,
    `inventory_id` int(11),
    `item_desc` varchar(45),
    `item_price` double,
    `item_num` int(11),
    `url` varchar(45),
    primary key (`item_id`),
    foreign key (`inventory_id`) references inventory(`inventory_id`)
);

DROP TABLE IF EXISTS `cart_item`;
create table `cart_item` (
	`cart_id` int(11) NOT NULL,
    `item_id` int(11) NOT NULL,
    `item_num` int(11) NOT NULL,
    primary key (`cart_id`, `item_id`),
    foreign key (`cart_id`) references cart_item(`cart_id`),
    foreign key (`item_id`) references item(`item_id`)
);
