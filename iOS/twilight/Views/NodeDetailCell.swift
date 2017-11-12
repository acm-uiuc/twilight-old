//
//  NodeDetailCell.swift
//  twilight
//
//  Created by Rauhul Varma on 11/12/17.
//  Copyright © 2017 acm. All rights reserved.
//

import Foundation
import UIKit

class NodeDetailCell: UITableViewCell {
    @IBOutlet weak var serialNumberLabel: UILabel!
    @IBOutlet weak var ipAddressLabel:    UILabel!
    @IBOutlet weak var dateAddedLabel:    UILabel!


    override func prepareForReuse() {
        super.prepareForReuse()
        serialNumberLabel.text = "Serial Number"
        ipAddressLabel.text = "IP Address"
        dateAddedLabel.text = "Date Added"
    }
}
