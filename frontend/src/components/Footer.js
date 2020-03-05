import React, { Component } from 'react';
import '../stylesheets/Footer.css';
class Footer extends Component {
render() {
return (
<footer className="footer ">
    <div className="container">
        <div className="row footer-top">
            <div className="col-md-6  col-lg-5 col-lg-offset-1">
                <div className="row about">
                    <div className="col-md-6 col-sm-3">
                        <h4>
                        本站信息
                        </h4>
                        <ul>
                            <li>
                                <a href="/about"  target="_self">
                                    简介
                                </a>
                            </li>
                            <li>
                                <a href="/legal" target="_self">
                                    免责声明
                                </a>
                            </li>
                        </ul>
                    </div>
                    <div className="col-md-6 col-sm-3">
                        <h4>
                        相关链接
                        </h4>
                        <ul>
                            <li>
                                <a href="/" target="_self">
                                    首页
                                </a>
                            </li>
                            <li>
                                <a href="/blog" target="_self">
                                    技术文章
                                </a>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
        <hr/>
        <div className="row footer-bottom list-inline text-center">
            freeiptv.cn 版权所有@ 2019 京ICP备19007292号-2
            <br />本站所有内容均来自网络。如侵犯了您的权利，请联系我们删除，感谢您的支持。
        </div>
    </div>
</footer>
);
}
}
export default Footer;