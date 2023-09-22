db = db.getSiblingDB('kinit'); // 切换到要创建的数据库

db.createUser({
  user: 'kinit',
  pwd: '123456',
  roles: ["readWrite", "dbAdmin"]
});