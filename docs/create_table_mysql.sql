/*==============================================================*/
/* Table: user 用户表                                                  */
/*==============================================================*/
create table user
(
   U_id                 int not null auto_increment,
   U_name               varchar(20) not null,
   U_passwd             varchar(20) not null,
   U_time               datetime not null,
   U_banned             bool not null,
   U_is_staff           bool not null,
   primary key (U_id)
);



/*==============================================================*/
/* Table: video 视频表                                            */
/*==============================================================*/
create table video
(
   V_id                 int not null auto_increment,
   V_addr               varchar(30) not null,
   V_name               varchar(50) not null,
   V_intro              varchar(255),
   V_time               datetime not null,
   U_id                 int not null,
   primary key (V_id)
);

alter table video add constraint FK_user_video foreign key (U_id)
      references user (U_id) on delete cascade on update cascade;



/*==============================================================*/
/* Table: comment 评论表                                         */
/*==============================================================*/
create table comment
(
   C_id                 int not null auto_increment,
   C_content            varchar(255) not null,
   C_time               datetime not null,
   U_id                 int not null,
   V_id                 int not null,
   primary key (C_id)
);

alter table comment add constraint FK_user_comment foreign key (U_id)
      references user (U_id) on delete cascade on update cascade;

alter table comment add constraint FK_video_comment foreign key (V_id)
      references video (V_id) on delete cascade on update cascade;
      


/*==============================================================*/
/* Table: reply 回复表                                            */
/*==============================================================*/
create table reply
(
   R_id                 int not null auto_increment,
   R_content            varchar(255) not null,
   R_time               datetime not null,
   U_subject_id         int not null,
   C_id                 int not null,
   U_object_id          int,
   primary key (R_id)
);

alter table reply add constraint FK_comment_reply foreign key (C_id)
      references comment (C_id) on delete cascade on update cascade;

alter table reply add constraint FK_userObject_reply foreign key (U_object_id)
      references user (U_id) on delete cascade on update cascade;

alter table reply add constraint FK_userSubject_reply foreign key (U_subject_id)
      references user (U_id) on delete cascade on update cascade;
      
      

/*==============================================================*/
/* Table: noticeC 评论通知表                                       */
/*==============================================================*/
create table noticeC
(
   NC_id                int not null auto_increment,
   NC_time              datetime not null,
   NC_read              bool not null,
   U_id                 int not null,
   C_id                 int not null,
   primary key (NC_id)
);

alter table noticeC add constraint FK_comment_noticeC foreign key (C_id)
      references comment (C_id) on delete cascade on update cascade;

alter table noticeC add constraint FK_user_noticeC foreign key (U_id)
      references user (U_id) on delete cascade on update cascade;



/*==============================================================*/
/* Table: noticeR 回复通知                                          */
/*==============================================================*/
create table noticeR
(
   NR_id                int not null auto_increment,
   NR_time              datetime not null,
   NR_read              bool not null,
   U_id                 int not null,
   R_id                 int not null,
   primary key (NR_id)
);

alter table noticeR add constraint FK_reply_noticeR foreign key (R_id)
      references reply (R_id) on delete cascade on update cascade;

alter table noticeR add constraint FK_user_noticeR foreign key (U_id)
      references user (U_id) on delete cascade on update cascade;