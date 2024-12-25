from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('users', 'XXXX_previous_migration'),  # 替换为实际的前一个迁移
    ]

    operations = [
        migrations.RunSQL(
            # 先删除原有约束
            "ALTER TABLE users_profile_score DROP FOREIGN KEY users_profile_score_user_id_64498e2f_fk_users_user_id;",
            # 回滚时重新创建原有约束
            "ALTER TABLE users_profile_score ADD CONSTRAINT users_profile_score_user_id_64498e2f_fk_users_user_id FOREIGN KEY (user_id) REFERENCES users_user(id);"
        ),
        migrations.RunSQL(
            # 添加新的 CASCADE 约束
            """
            ALTER TABLE users_profile_score 
            ADD CONSTRAINT users_profile_score_user_id_fk 
            FOREIGN KEY (user_id) 
            REFERENCES users_user(id) 
            ON DELETE CASCADE;
            """,
            # 回滚时删除约束
            "ALTER TABLE users_profile_score DROP FOREIGN KEY users_profile_score_user_id_fk;"
        ),
    ] 