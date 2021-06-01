DATABASES = {
    'default': {
        'ATOMIC_REQUESTS': True,
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'spug',  # 替换为自己的数据库名，请预先创建好编码为utf8mb4的数据库
        'USER': 'root',  # 数据库用户名
        'PASSWORD': '123',  # 数据库密码
        'HOST': '192.168.8.232',  # 数据库地址
        'OPTIONS': {
            'charset': 'utf8mb4',
            'sql_mode': 'STRICT_TRANS_TABLES'
        }
    }
}
