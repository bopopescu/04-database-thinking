DROP DATABASE IF EXISTS `chat_app`;
CREATE DATABASE IF NOT EXISTS `chat_app`;
USE `chat_app`;

DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
   `id` int unsigned auto_increment,
   `username` varchar(100) not null,
   `password` varchar(100) not null,
   `email` varchar(100) not null,
   `created_at` timestamp not null default current_timestamp,
   `is_active` boolean default false,
   
   primary key(`id`),
   unique (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;



DROP TABLE IF EXISTS `relationship`;
CREATE TABLE `friends` (
   `userid_1` int unsigned,
   `userid_2` int unsigned,
   `status` tinyint not null,
   `action_user` int unsigned not null,
   `created_at` timestamp not null default current_timestamp,
   
   primary key(`userid_1`,`userid_2`),
   constraint `check_PK` check(`userid_1` < `userid_2`), 
   foreign key(`userid_1`) references `users` (`id`),
   foreign key(`userid_2`) references `users` (`id`),
   foreign key(`action_user`) references `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS `conversation`;
CREATE TABLE `conversation` (
   `id` int unsigned auto_increment,
   `title` varchar(100),
   `creator_id` int unsigned not null,
   `created_at` timestamp not null default current_timestamp,
   `is_group` boolean not null default true,
   
   primary key(`id`),
   foreign key(`creator_id`) references `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS `participants`;
CREATE TABLE `participants` (
   `id` int unsigned auto_increment,
   `conversation_id` int unsigned not null,
   `user_id` int unsigned not null,
   `created_at` timestamp not null default current_timestamp,
   
   primary key(`id`),
   foreign key(`conversation_id`) references `conversation` (`id`),
   foreign key(`user_id`) references `users` (`id`),
   unique (`conversation_id`,`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;



DROP TABLE IF EXISTS `messages`;
CREATE TABLE `messages` (
   `id` int unsigned auto_increment,
   `conversation_id` int unsigned not null,
   `sender_id` int unsigned not null,
   `message` varchar(255) not null,
   `created_at` timestamp not null default current_timestamp,
   
   primary key(`id`),
   foreign key(`conversation_id`) references `conversation` (`id`),
   foreign key(`sender_id`) references `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;



DROP TABLE IF EXISTS `message_status`;
CREATE TABLE `message_status` (
   `id` int unsigned auto_increment,
   `conversation_id` int unsigned not null,
   `message_id` int unsigned not null,
   `receiver_id` int unsigned not null,
   `is_seen` boolean not null default false,
   
   primary key(`id`),
   foreign key(`conversation_id`) references `conversation` (`id`),
   foreign key(`message_id`) references `messages` (`id`),
   foreign key(`receiver_id`) references `users` (`id`),
   unique(`conversation_id`,`message_id`,`receiver_id`)
   
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;



#CALL `chat_app`.`insert_fetch_conversation`('ddd', 4);
insert INTO `users` (`username`,`password`,`email`,`is_active`) 
values ('x','x','x',false);

insert INTO `users` (`username`,`password`,`email`,`is_active`) 
values ('y','y','y',false);

insert INTO `users` (`username`,`password`,`email`,`is_active`) 
values ('z','z','z',false);

insert INTO `users` (`username`,`password`,`email`,`is_active`) 
values ('t','t','t',false);

insert into `conversation` (`title`,`creator_id`) 
values ('hello1',1);

insert into `conversation` (`title`,`creator_id`) 
values ('hello2',1);

insert into `conversation` (`title`,`creator_id`,`is_group`) 
values ('z-t',3,false);

insert into `participants`(`conversation_id`,`user_id`)
values (1, 1);
insert into `participants`(`conversation_id`,`user_id`)
values (1, 2);
insert into `participants`(`conversation_id`,`user_id`)
values (2, 1);
insert into `participants`(`conversation_id`,`user_id`)
values (1, 3);

insert into `participants`(`conversation_id`,`user_id`)
values (3, 3);
insert into `participants`(`conversation_id`,`user_id`)
values (3, 4);

-- INSERT INTO `messages`(`conversation_id`,`sender_id`,`message`)VALUES(1,1,'xxyyzz');
-- INSERT INTO `messages`(`conversation_id`,`sender_id`,`message`)VALUES(2,1,'aabbcc');
-- INSERT INTO `messages`(`conversation_id`,`sender_id`,`message`)VALUES(3,3,'cclemon');


-- USE `chat_app`;
-- DROP procedure IF EXISTS `insert_private_chat`;
-- 
-- DELIMITER $$
-- USE `chat_app`$$
-- CREATE procedure `insert_private_chat` (IN d_title varchar(100),IN d_user1_id INT, IN d_username2 varchar(100))
-- BEGIN
-- 
-- INSERT INTO `conversation` (`title`,`creator_id`,`is_group`) VALUES (d_title,d_user1_id,false);
-- 
-- SELECT @c_id := `id` FROM `conversation` WHERE `title` = d_title AND `is_group`=false;
-- 
-- INSERT INTO `participants` (`conversation_id`,`user_id`) VALUES (@c_id, d_user1_id);
-- 
-- SELECT @u_id := `id` FROM `users` WHERE `username` = d_username2;
-- 
-- INSERT INTO `participants` (`conversation_id`,`user_id`) VALUES (@c_id, @u_id);
-- 
-- COMMIT;
-- 
-- END$$
-- 
-- DELIMITER ;

