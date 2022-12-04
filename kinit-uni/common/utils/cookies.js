const TokenKey = 'Admin-Token'

// 获取客户端token
export function getToken() {
    try {
        const value = uni.getStorageSync(TokenKey);
        if (value) {
			return value;
        }
		return ""
    } catch (e) {
        // error
		return ""
    }
}

// 设置客户端token
export function setToken(token) {
    uni.setStorage({
		key: TokenKey,
		data: token,
		success: function (res) {
			console.log('成功存储token');
		},
		fail:function(e){
			console.log(e)
			console.log("存储token失败");
		}
	});
}

// 删除客户端token
export function removeToken() {
    uni.removeStorage({
    	key: TokenKey,
    	success: function (res) {
    		console.log('成功删除token');
    	}
    });
}

// 获取客户端
export function getStorage(key) {
    try {
        const value = uni.getStorageSync(key);
        if (value) {
            // console.log("成功获取到 Storage：", value);
			return value;
        }
		return ""
    } catch (e) {
        // error
		return ""
    }
}

// 设置客户端 Storage
export function setStorage(key, value) {
    uni.setStorage({
		key: key,
		data: value,
		success: function (res) {
			console.log('成功存储');
		},
		fail:function(e){
			console.log(e)
			console.log("存储失败");
		}
	});
}

// 删除客户端 Storage
export function removeStorage(key) {
    uni.removeStorage({
    	key: key,
    	success: function (res) {
    		console.log('成功删除Storage');
    	}
    });
}