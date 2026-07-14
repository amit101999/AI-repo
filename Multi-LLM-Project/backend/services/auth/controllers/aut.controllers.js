import User from '../models/user.model.js';

export const login = (req, res) => {
    const { username, password } = req.body;
    if (!username || !password) {
        return res.status(400).json({ message: 'Username and password are required' });
    }

    const user = User.findByUsername(username);
    if (!user) {
        return res.status(401).json({ message: 'Invalid username or password' });
    }

    const pass = 
    
}
