import React, { Component } from 'react';
import '../stylesheets/Header.css';

class Header extends Component {

    render() {

        return (

            <header id="header">
                <div className="wrapper">
                    <a href="/" className="brand" title="免费IPTV网络电视资源">FreeIPTV.CN</a>
                    <button id="headerMenu" className="menu">
                        <i className="fa fa-bars"></i>
                    </button>
                    <nav id="headerNav" className="navlist">
                        <ul>
                            <li>
                                <a href="/" className="nav_a active">首页</a>
                            </li>
                            <li>
                                <a href="/channels" className="nav_a ">频道搜索</a>
                            </li>
                            <li>
                                <a href="/blog/" className="nav_a ">技术文章</a>
                            </li>
                            <li>
                                <a href="/blog/category/#IPTV工具" className="nav_a">IPTV工具</a>
                            </li>
                        </ul>
                    </nav>
                </div>
            </header>
            );
    }
}


export default Header;
