//
//  LoginAwareTabBarController.swift
//  twilight
//
//  Created by Rauhul Varma on 11/11/17.
//  Copyright © 2017 acm. All rights reserved.
//

import UIKit

class LoginAwareTabBarController: UITabBarController {

    override func viewDidAppear(_ animated: Bool) {
        super.viewDidAppear(animated)

        LoginController.shared.presentLoginViewController(ifNeeded: false, fromViewController: self)
    }




}
