<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN"
   "http://www.w3.org/TR/html4/strict.dtd">

<html lang="en">
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
	<title>Login</title>
</head>
<body>
<form action="/login/signin" method="post">
    <table>
        <tr>
            <td class="label">
                <label for="username">User Name:</label>
            </td>
            <td class="field">
                <input type="text" id="username" name="username"/>
            </td>
        </tr>
        <tr>
            <td class="label">
                <label for="password">Password:</label>
            </td>
            <td class="field">
                <input type="password" id="password" name="password"/>
            </td>
        </tr>
        <tr>
            <td colspan="2" class="buttons">
                <input type="submit" name="login" value="Login"/>
            </td>
        </tr>
    </table>
</form>

</body>
</html>
