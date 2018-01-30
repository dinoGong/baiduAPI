# baiduAPI




uids

20180001: YZ
20180002: ZX
20180003: HYX




Flask+mariadb+baidu-aip



mariadb:
https://wiki.archlinux.org/index.php/MySQL_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87)

工具：
dbeaver




CREATE TABLE `member`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NULL,
  `passwd` VARCHAR(45) NULL,
  `face_url` VARCHAR(200) NULL,
  `face_id` INT NULL,
  PRIMARY KEY (`id`));
