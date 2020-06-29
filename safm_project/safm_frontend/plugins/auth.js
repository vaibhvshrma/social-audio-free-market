const Cookie = process.client ? require('js-cookie') : undefined

export default ({ nuxt, store, $axios }, inject) => {
    // Stores the user authentication information
    inject('authenticateUser', (response) => {
        const authToken = response.data.token
        const userid = response.data.userid
        const username = response.data.username

        store.commit('setAuth', authToken)
        Cookie.set('auth', authToken)

        store.commit('setUser', {
            id: userid,
            name: username
        })
        Cookie.set('userid', userid)
        Cookie.set('username', username)

        $axios.setHeader('Authorization', `Token ${authToken}`)

        return userid
    })

    // Removes the user authentication information
    inject('logoutUser', async () => {
        await $axios.post('/logout')

        store.commit('setAuth', null)
        Cookie.remove('auth')
        store.commit('setUser', null)
        Cookie.remove('userid')
        Cookie.remove('username')

        $axios.setHeader('Authorization', '')
    })
}
