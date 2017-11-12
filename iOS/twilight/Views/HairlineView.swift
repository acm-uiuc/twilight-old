//
//  HairlineView.swift
//  twilight
//
//  Created by Rauhul Varma on 11/12/17.
//  Copyright © 2017 acm. All rights reserved.
//

import Foundation
import UIKit

class HairlineView: UIView {

    @IBOutlet weak var hairlineConstraint: NSLayoutConstraint?

    override func awakeFromNib() {
        hairlineConstraint?.constant = 1 / UIScreen.main.scale
    }

}
