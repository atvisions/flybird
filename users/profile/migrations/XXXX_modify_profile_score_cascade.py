from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('users', '0001_initial'),  # 替换为你的最后一个迁移
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            ALTER TABLE users_profile_score 
            DROP FOREIGN KEY users_profile_score_user_id_64498e2f_fk_users_user_id;
            
            ALTER TABLE users_profile_score 
            ADD CONSTRAINT users_profile_score_user_id_64498e2f_fk_users_user_id 
            FOREIGN KEY (user_id) 
            REFERENCES users_user(id) 
            ON DELETE CASCADE;
            """,
            reverse_sql="""
            ALTER TABLE users_profile_score 
            DROP FOREIGN KEY users_profile_score_user_id_64498e2f_fk_users_user_id;
            
            ALTER TABLE users_profile_score 
            ADD CONSTRAINT users_profile_score_user_id_64498e2f_fk_users_user_id 
            FOREIGN KEY (user_id) 
            REFERENCES users_user(id);
            """
        )
    ] 